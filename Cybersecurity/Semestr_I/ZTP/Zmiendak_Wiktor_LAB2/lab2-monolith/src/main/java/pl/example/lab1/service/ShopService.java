package pl.example.lab1.service;

import pl.example.lab1.dto.OrderCreateRequest;
import pl.example.lab1.dto.ProductCreateRequest;
import pl.example.lab1.model.Product;
import pl.example.lab1.model.ShopOrder;

import java.util.List;

public interface ShopService {
    List<Product> getProducts();

    Product getProductById(long id);

    Product createProduct(ProductCreateRequest req);

    List<ShopOrder> getOrders();

    ShopOrder getOrderById(long id);

    ShopOrder createOrder(OrderCreateRequest req);
}
