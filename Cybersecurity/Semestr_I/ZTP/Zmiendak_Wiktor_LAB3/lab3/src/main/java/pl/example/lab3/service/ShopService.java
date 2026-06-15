package pl.example.lab3.service;

import pl.example.lab3.dto.OrderCreateRequest;
import pl.example.lab3.dto.ProductCreateRequest;
import pl.example.lab3.model.Product;
import pl.example.lab3.model.ShopOrder;

import java.util.List;

public interface ShopService {

    List<Product> getProducts();

    Product getProductById(Long id);

    Product createProduct(ProductCreateRequest request);

    List<ShopOrder> getOrders();

    ShopOrder getOrderById(Long id);

    ShopOrder createOrder(OrderCreateRequest request);
}
