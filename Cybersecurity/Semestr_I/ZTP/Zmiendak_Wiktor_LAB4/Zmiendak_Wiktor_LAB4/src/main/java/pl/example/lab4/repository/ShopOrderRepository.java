package pl.example.lab4.repository;

import pl.example.lab4.model.ShopOrder;

public interface ShopOrderRepository {

    ShopOrder save(ShopOrder order);
}
