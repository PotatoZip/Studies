package pl.example.lab3.entity;

import jakarta.persistence.*;

import java.time.Instant;

@Entity
@Table(name = "shop_orders")
public class ShopOrderEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "product_id")
    private ProductEntity product;

    @Column(nullable = false)
    private int quantity;

    @Column(nullable = false)
    private double total;

    @Column(nullable = false)
    private Instant createdAt;

    public ShopOrderEntity() {
    }

    public ShopOrderEntity(Long id, ProductEntity product, int quantity, double total, Instant createdAt) {
        this.id = id;
        this.product = product;
        this.quantity = quantity;
        this.total = total;
        this.createdAt = createdAt;
    }

    public ShopOrderEntity(ProductEntity product, int quantity, double total, Instant createdAt) {
        this.product = product;
        this.quantity = quantity;
        this.total = total;
        this.createdAt = createdAt;
    }

    public Long getId() {
        return id;
    }

    public ProductEntity getProduct() {
        return product;
    }

    public int getQuantity() {
        return quantity;
    }

    public double getTotal() {
        return total;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setProduct(ProductEntity product) {
        this.product = product;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public void setTotal(double total) {
        this.total = total;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }
}