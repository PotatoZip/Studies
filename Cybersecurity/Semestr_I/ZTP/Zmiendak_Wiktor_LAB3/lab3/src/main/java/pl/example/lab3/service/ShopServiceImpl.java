package pl.example.lab3.service;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import pl.example.lab3.dto.OrderCreateRequest;
import pl.example.lab3.dto.ProductCreateRequest;
import pl.example.lab3.entity.ProductEntity;
import pl.example.lab3.entity.ShopOrderEntity;
import pl.example.lab3.mapper.ShopMapper;
import pl.example.lab3.model.Product;
import pl.example.lab3.model.ShopOrder;
import pl.example.lab3.repository.ProductRepository;
import pl.example.lab3.repository.ShopOrderRepository;

import java.time.Instant;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ShopServiceImpl implements ShopService {

    private final ProductRepository productRepository;
    private final ShopOrderRepository shopOrderRepository;
    private final ShopMapper shopMapper;

    public ShopServiceImpl(ProductRepository productRepository,
            ShopOrderRepository shopOrderRepository,
            ShopMapper shopMapper) {
        this.productRepository = productRepository;
        this.shopOrderRepository = shopOrderRepository;
        this.shopMapper = shopMapper;
    }

    @Override
    public List<Product> getProducts() {
        return productRepository.findAll()
                .stream()
                .map(shopMapper::toModel)
                .collect(Collectors.toList());
    }

    @Override
    public Product getProductById(Long id) {
        ProductEntity entity = productRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Product not found"));
        return shopMapper.toModel(entity);
    }

    @Override
    public Product createProduct(ProductCreateRequest request) {
        ProductEntity entity = new ProductEntity(
                request.getName(),
                request.getPrice(),
                request.getStock());
        ProductEntity saved = productRepository.save(entity);
        return shopMapper.toModel(saved);
    }

    @Override
    public List<ShopOrder> getOrders() {
        return shopOrderRepository.findAll()
                .stream()
                .map(shopMapper::toModel)
                .collect(Collectors.toList());
    }

    @Override
    public ShopOrder getOrderById(Long id) {
        ShopOrderEntity entity = shopOrderRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Order not found"));
        return shopMapper.toModel(entity);
    }

    @Override
    @Transactional
    public ShopOrder createOrder(OrderCreateRequest request) {
        ProductEntity product = productRepository.findById(request.getProductId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Product not found"));

        if (product.getStock() < request.getQuantity()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Insufficient stock");
        }

        product.setStock(product.getStock() - request.getQuantity());
        productRepository.save(product);

        double total = product.getPrice() * request.getQuantity();
        ShopOrderEntity orderEntity = new ShopOrderEntity(
                product,
                request.getQuantity(),
                total,
                Instant.now());
        ShopOrderEntity savedOrder = shopOrderRepository.save(orderEntity);
        return shopMapper.toModel(savedOrder);
    }
}
