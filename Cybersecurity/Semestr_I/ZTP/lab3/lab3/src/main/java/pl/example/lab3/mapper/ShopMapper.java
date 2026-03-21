package pl.example.lab3.mapper;

import org.springframework.stereotype.Component;
import pl.example.lab3.entity.ProductEntity;
import pl.example.lab3.entity.ShopOrderEntity;
import pl.example.lab3.model.Product;
import pl.example.lab3.model.ShopOrder;

@Component
public class ShopMapper {

    public Product toModel(ProductEntity entity) {
        return new Product(
                entity.getId(),
                entity.getName(),
                entity.getPrice(),
                entity.getStock()
        );
    }

    public ShopOrder toModel(ShopOrderEntity entity) {
        return new ShopOrder(
                entity.getId(),
                entity.getProduct().getId(),
                entity.getQuantity(),
                entity.getTotal(),
                entity.getCreatedAt() == null ? null : entity.getCreatedAt().toString()
        );
    }
}
