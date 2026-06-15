package pl.example.lab4.service;

import pl.example.lab4.model.OrderDraft;
import pl.example.lab4.model.Product;
import pl.example.lab4.model.ShopOrder;
import pl.example.lab4.repository.ProductRepository;
import pl.example.lab4.repository.ShopOrderRepository;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Clock;
import java.time.Instant;
import java.util.NoSuchElementException;

public class ShopServiceImpl implements ShopService {

    private final ProductRepository productRepository;
    private final ShopOrderRepository shopOrderRepository;
    private final PricingPolicy pricingPolicy;
    private final Clock clock;

    public ShopServiceImpl(ProductRepository productRepository,
            ShopOrderRepository shopOrderRepository,
            PricingPolicy pricingPolicy,
            Clock clock) {
        this.productRepository = productRepository;
        this.shopOrderRepository = shopOrderRepository;
        this.pricingPolicy = pricingPolicy;
        this.clock = clock;
    }

    @Override
    public ShopOrder placeOrder(OrderDraft draft) {
        // Validation phase (all checks before any state modification)
        if (draft.getQuantity() <= 0) {
            throw new IllegalArgumentException("Quantity must be greater than 0");
        }

        Product product = productRepository.findById(draft.getProductId())
                .orElseThrow(() -> new NoSuchElementException("Product not found"));

        if (product.getStock() < draft.getQuantity()) {
            throw new IllegalStateException("Insufficient stock");
        }

        // Calculation phase
        BigDecimal subtotalAmount = subtotal(product, draft.getQuantity());
        BigDecimal discount = pricingPolicy.calculateDiscount(product, draft.getQuantity(), draft.getDiscountCode());
        BigDecimal subtotalAfterDiscount = subtotalAmount.subtract(discount);
        BigDecimal shipping = pricingPolicy.calculateShipping(subtotalAfterDiscount);
        BigDecimal total = subtotalAfterDiscount.add(shipping);
        int loyaltyPoints = pricingPolicy.calculateLoyaltyPoints(total);
        Instant createdAt = now();

        // State modification phase
        product.decreaseStock(draft.getQuantity());
        productRepository.save(product);

        ShopOrder order = new ShopOrder(
                null,
                draft.getProductId(),
                draft.getQuantity(),
                subtotalAmount,
                discount,
                shipping,
                total,
                loyaltyPoints,
                createdAt);

        return shopOrderRepository.save(order);
    }

    private BigDecimal subtotal(Product product, int quantity) {
        return product.getPrice()
                .multiply(BigDecimal.valueOf(quantity))
                .setScale(2, RoundingMode.HALF_UP);
    }

    private Instant now() {
        return Instant.now(clock);
    }
}
