package pl.example.lab9.orderservice;

import java.util.List;

public interface OrderService {

  Order createOrder(long productId, int quantity);

  Order getOrder(long id);

  List<Order> getOrders();
}
