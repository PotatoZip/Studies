package pl.example.lab4;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.InOrder;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import pl.example.lab4.model.OrderDraft;
import pl.example.lab4.model.Product;
import pl.example.lab4.model.ShopOrder;
import pl.example.lab4.repository.ProductRepository;
import pl.example.lab4.repository.ShopOrderRepository;
import pl.example.lab4.service.DefaultPricingPolicy;
import pl.example.lab4.service.ShopServiceImpl;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class Lab4Grade4UnitTest {

    @Mock
    ProductRepository productRepository;

    @Mock
    ShopOrderRepository shopOrderRepository;

    @Captor
    ArgumentCaptor<ShopOrder> orderCaptor;

    @Test
    @DisplayName("4.0/1 BULK5 daje 5% tylko dla quantity >= 5")
    void bulk5ShouldApplyOnlyForFiveOrMoreItems() {
        DefaultPricingPolicy pricingPolicy = new DefaultPricingPolicy();
        Product product = product(1L, "SSD", "50.00", 20);

        assertEquals(money("0.00"), pricingPolicy.calculateDiscount(product, 4, "BULK5"));
        assertEquals(money("12.50"), pricingPolicy.calculateDiscount(product, 5, "BULK5"));
    }

    @Test
    @DisplayName("4.0/2 VIP daje 15%, darmowa dostawa od 300.00 i punkty to floor(total / 10)")
    void vipDiscountShippingAndPointsShouldBeCalculatedCorrectly() {
        DefaultPricingPolicy pricingPolicy = new DefaultPricingPolicy();
        Product product = product(1L, "Laptop", "100.00", 10);

        BigDecimal discount = pricingPolicy.calculateDiscount(product, 4, "VIP");
        BigDecimal discountedSubtotal = money("400.00").subtract(discount);
        BigDecimal shipping = pricingPolicy.calculateShipping(discountedSubtotal);
        int points = pricingPolicy.calculateLoyaltyPoints(discountedSubtotal.add(shipping));

        assertEquals(money("60.00"), discount);
        assertEquals(money("0.00"), shipping);
        assertEquals(34, points);
    }

    @Test
    @DisplayName("4.0/3 dostawa za 15.00 poniżej progu darmowej dostawy")
    void shippingShouldCostFifteenBelowFreeShippingThreshold() {
        DefaultPricingPolicy pricingPolicy = new DefaultPricingPolicy();

        assertEquals(money("15.00"), pricingPolicy.calculateShipping(money("299.99")));
        assertEquals(money("0.00"), pricingPolicy.calculateShipping(money("300.00")));
    }

    @Test
    @DisplayName("4.0/4 placeOrder korzysta z Clock i zapisuje produkt przed zamówieniem")
    void placeOrderShouldUseClockAndPersistEntitiesInCorrectOrder() {
        Clock fixedClock = Clock.fixed(Instant.parse("2026-04-01T08:00:00Z"), ZoneOffset.UTC);
        DefaultPricingPolicy pricingPolicy = new DefaultPricingPolicy();
        ShopServiceImpl service = new ShopServiceImpl(productRepository, shopOrderRepository, pricingPolicy, fixedClock);
        Product product = product(1L, "Laptop", "120.00", 10);

        when(productRepository.findById(1L)).thenReturn(Optional.of(product));
        when(productRepository.save(product)).thenReturn(product);
        when(shopOrderRepository.save(any(ShopOrder.class))).thenAnswer(invocation -> {
            ShopOrder order = invocation.getArgument(0);
            return new ShopOrder(
                    77L,
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

        ShopOrder result = service.placeOrder(new OrderDraft(1L, 3, "VIP"));

        verify(shopOrderRepository).save(orderCaptor.capture());
        ShopOrder savedOrder = orderCaptor.getValue();
        assertEquals(Instant.parse("2026-04-01T08:00:00Z"), savedOrder.getCreatedAt());
        assertEquals(money("360.00"), savedOrder.getSubtotal());
        assertEquals(money("54.00"), savedOrder.getDiscountAmount());
        assertEquals(money("0.00"), savedOrder.getShippingCost());
        assertEquals(money("306.00"), savedOrder.getTotal());
        assertEquals(30, savedOrder.getLoyaltyPoints());
        assertEquals(7, product.getStock());

        InOrder inOrder = inOrder(productRepository, shopOrderRepository);
        inOrder.verify(productRepository).findById(1L);
        inOrder.verify(productRepository).save(product);
        inOrder.verify(shopOrderRepository).save(any(ShopOrder.class));

        assertEquals(77L, result.getId());
    }

    @Test
    @DisplayName("4.0/5 błędne zamówienie nie zapisuje produktu ani zamówienia")
    void invalidOrderShouldNotPersistAnything() {
        Clock fixedClock = Clock.fixed(Instant.parse("2026-04-01T08:00:00Z"), ZoneOffset.UTC);
        DefaultPricingPolicy pricingPolicy = new DefaultPricingPolicy();
        ShopServiceImpl service = new ShopServiceImpl(productRepository, shopOrderRepository, pricingPolicy, fixedClock);
        Product product = product(5L, "Router", "200.00", 1);
        when(productRepository.findById(5L)).thenReturn(Optional.of(product));

        IllegalStateException exception = assertThrows(
                IllegalStateException.class,
                () -> service.placeOrder(new OrderDraft(5L, 2, "VIP"))
        );

        assertEquals("Insufficient stock", exception.getMessage());
        verify(productRepository).findById(5L);
        verify(productRepository, never()).save(any());
        verifyNoInteractions(shopOrderRepository);
        assertEquals(1, product.getStock(), "Stock nie powinien się zmienić po odrzuconym zamówieniu");
    }

    private static Product product(Long id, String name, String price, int stock) {
        return new Product(id, name, money(price), stock);
    }

    private static BigDecimal money(String value) {
        return new BigDecimal(value).setScale(2);
    }
}
