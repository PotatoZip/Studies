package pl.example.lab1.service;

import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import pl.example.lab1.dto.OrderCreateRequest;
import pl.example.lab1.dto.ProductCreateRequest;
import pl.example.lab1.model.Product;
import pl.example.lab1.model.ShopOrder;
import pl.example.lab1.store.InMemoryStore;

import java.time.Instant;
import java.util.List;

import static org.springframework.http.HttpStatus.BAD_REQUEST;
import static org.springframework.http.HttpStatus.NOT_FOUND;

@Service
public class ShopServiceImpl implements ShopService {

    private final InMemoryStore store;

    public ShopServiceImpl(InMemoryStore store) {
        this.store = store;
    }

    @Override
    public List<Product> getProducts() {
        return store.getProducts().values().stream().toList();
    }

    @Override
    public Product getProductById(long id) {
        Product product = store.getProducts().get(id);
        if (product == null) {
            throw new ResponseStatusException(NOT_FOUND, "Product not found");
        }
        return product;
    }

    @Override
    public Product createProduct(ProductCreateRequest req) {
        long id = store.generateNextProductId();
        Product product = new Product(id, req.getName(), req.getPrice(), req.getStock());
        store.getProducts().put(id, product);
        return product;
    }

    @Override
    public List<ShopOrder> getOrders() {
        return store.getOrders().values().stream().toList();
    }

    @Override
    public ShopOrder getOrderById(long id) {
        ShopOrder order = store.getOrders().get(id);
        if (order == null) {
            throw new ResponseStatusException(NOT_FOUND, "Order not found");
        }
        return order;
    }

    @Override
    public ShopOrder createOrder(OrderCreateRequest req) {
        Product product = store.getProducts().get(req.getProductId());
        if (product == null) {
            throw new ResponseStatusException(NOT_FOUND, "Product not found");
        }

        int quantity = req.getQuantity();
        if (quantity > product.getStock()) {
            throw new ResponseStatusException(BAD_REQUEST, "Insufficient stock");
        }

        product.setStock(product.getStock() - quantity);
        double total = product.getPrice() * quantity;

        long orderId = store.generateNextOrderId();
        ShopOrder order = new ShopOrder(orderId, req.getProductId(), quantity, total, Instant.now().toString());
        store.getOrders().put(orderId, order);
        return order;
    }
}
