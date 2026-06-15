package pl.example.lab4.service;

import pl.example.lab4.model.OrderDraft;
import pl.example.lab4.model.ShopOrder;

public interface ShopService {

    ShopOrder placeOrder(OrderDraft draft);
}
