package pl.example.lab4;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import pl.example.lab4.model.OrderDraft;
import pl.example.lab4.model.Product;
import pl.example.lab4.model.ShopOrder;
import pl.example.lab4.repository.ProductRepository;
import pl.example.lab4.repository.ShopOrderRepository;
import pl.example.lab4.service.DefaultPricingPolicy;
import pl.example.lab4.service.PricingPolicy;
import pl.example.lab4.service.ShopServiceImpl;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.NoSuchElementException;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class Lab4Grade3UnitTest {

    @Mock
    ProductRepository productRepository;

    @Mock
    ShopOrderRepository shopOrderRepository;

    @Mock
    PricingPolicy pricingPolicy;

    @Captor
    ArgumentCaptor<ShopOrder> orderCaptor;

    @Test
    @DisplayName("3.0/1 SAVE10 daje 10% rabatu od subtotal")
    void save10ShouldReturnTenPercentDiscount() {
        DefaultPricingPolicy pricingPolicy = new DefaultPricingPolicy();
        Product product = product(1L, "Klawiatura", "100.00", 10);

        BigDecimal discount = pricingPolicy.calculateDiscount(product, 2, "SAVE10");

        assertEquals(money("20.00"), discount);
    }

    @Test
    @DisplayName("3.0/2 Nieznany kod rabatowy zwraca 0.00")
    void unknownCodeShouldReturnZeroDiscount() {
        DefaultPricingPolicy pricingPolicy = new DefaultPricingPolicy();
        Product product = product(1L, "Mysz", "80.00", 10);

        BigDecimal discount = pricingPolicy.calculateDiscount(product, 3, "SOMETHING_ELSE");

        assertEquals(money("0.00"), discount);
    }

    @Test
    @DisplayName("3.0/3 placeOrder zapisuje produkt i zamówienie oraz liczy subtotal i total")
    void placeOrderShouldPersistOrderAndDecreaseStock() {
        Clock fixedClock = Clock.fixed(Instant.parse("2026-03-22T10:15:30Z"), ZoneOffset.UTC);
        ShopServiceImpl service = new ShopServiceImpl(productRepository, shopOrderRepository, pricingPolicy, fixedClock);
        Product product = product(1L, "Laptop", "100.00", 10);

        when(productRepository.findById(1L)).thenReturn(Optional.of(product));
        when(pricingPolicy.calculateDiscount(product, 2, "SAVE10")).thenReturn(money("20.00"));
        when(pricingPolicy.calculateShipping(money("180.00"))).thenReturn(money("15.00"));
        when(pricingPolicy.calculateLoyaltyPoints(money("195.00"))).thenReturn(19);
        when(productRepository.save(product)).thenReturn(product);
        when(shopOrderRepository.save(any(ShopOrder.class))).thenAnswer(invocation -> {
            ShopOrder order = invocation.getArgument(0);
            return new ShopOrder(
                    1L,
                    order.getProductId(),
                    order.getQuantity(),
                    order.getSubtotal(),
                    order.getDiscountAmount(),
                    order.getShippingCost(),
                    order.getTotal(),
                    order.getLoyaltyPoints(),
                    order.getCreatedAt()
            );
        });

        ShopOrder result = service.placeOrder(new OrderDraft(1L, 2, "SAVE10"));

        assertEquals(8, product.getStock(), "Stock produktu powinien zostać zmniejszony");
        verify(productRepository).save(product);
        verify(shopOrderRepository).save(orderCaptor.capture());

        ShopOrder savedOrder = orderCaptor.getValue();
        assertEquals(1L, savedOrder.getProductId());
        assertEquals(2, savedOrder.getQuantity());
        assertEquals(money("200.00"), savedOrder.getSubtotal());
        assertEquals(money("20.00"), savedOrder.getDiscountAmount());
        assertEquals(money("15.00"), savedOrder.getShippingCost());
        assertEquals(money("195.00"), savedOrder.getTotal());
        assertEquals(19, savedOrder.getLoyaltyPoints());
        assertEquals(Instant.parse("2026-03-22T10:15:30Z"), savedOrder.getCreatedAt());

        assertEquals(1L, result.getId());
        assertEquals(money("195.00"), result.getTotal());
    }

    @Test
    @DisplayName("3.0/4 placeOrder odrzuca quantity <= 0")
    void placeOrderShouldRejectInvalidQuantity() {
        ShopServiceImpl service = new ShopServiceImpl(productRepository, shopOrderRepository, pricingPolicy, Clock.systemUTC());

        IllegalArgumentException exception = assertThrows(
                IllegalArgumentException.class,
                () -> service.placeOrder(new OrderDraft(1L, 0, "SAVE10"))
        );

        assertEquals("Quantity must be greater than 0", exception.getMessage());
        verifyNoInteractions(productRepository, shopOrderRepository, pricingPolicy);
    }

    @Test
    @DisplayName("3.0/5 placeOrder odrzuca brakujący produkt")
    void placeOrderShouldRejectMissingProduct() {
        ShopServiceImpl service = new ShopServiceImpl(productRepository, shopOrderRepository, pricingPolicy, Clock.systemUTC());
        when(productRepository.findById(999L)).thenReturn(Optional.empty());

        NoSuchElementException exception = assertThrows(
                NoSuchElementException.class,
                () -> service.placeOrder(new OrderDraft(999L, 1, null))
        );

        assertEquals("Product not found", exception.getMessage());
        verify(productRepository).findById(999L);
        verify(productRepository, never()).save(any());
        verifyNoInteractions(shopOrderRepository, pricingPolicy);
    }

    @Test
    @DisplayName("3.0/6 placeOrder odrzuca zamówienie przy zbyt małym stock")
    void placeOrderShouldRejectInsufficientStock() {
        ShopServiceImpl service = new ShopServiceImpl(productRepository, shopOrderRepository, pricingPolicy, Clock.systemUTC());
        Product product = product(1L, "Monitor", "999.00", 1);
        when(productRepository.findById(1L)).thenReturn(Optional.of(product));

        IllegalStateException exception = assertThrows(
                IllegalStateException.class,
                () -> service.placeOrder(new OrderDraft(1L, 2, null))
        );

        assertEquals("Insufficient stock", exception.getMessage());
        verify(productRepository).findById(1L);
        verify(productRepository, never()).save(any());
        verifyNoInteractions(shopOrderRepository, pricingPolicy);
    }

    private static Product product(Long id, String name, String price, int stock) {
        return new Product(id, name, money(price), stock);
    }

    private static BigDecimal money(String value) {
        return new BigDecimal(value).setScale(2);
    }
}
