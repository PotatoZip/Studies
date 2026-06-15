package pl.example.lab10.order;

import java.util.List;

public interface OrderService {

  Order createOrder(long productId, int quantity);

  Order getOrder(long id);

  List<Order> getOrders();
}
