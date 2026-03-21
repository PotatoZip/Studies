package pl.example.lab3.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public class ProductCreateRequest {

    @NotBlank(message = "Field 'name' is required")
    private String name;

    @NotNull(message = "Field 'price' is required")
    @Positive(message = "Field 'price' must be a number > 0")
    private Double price;

    @NotNull(message = "Field 'stock' is required")
    @Min(value = 0, message = "Field 'stock' must be an integer >= 0")
    private Integer stock;

    public ProductCreateRequest() {
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Double getPrice() {
        return price;
    }

    public void setPrice(Double price) {
        this.price = price;
    }

    public Integer getStock() {
        return stock;
    }

    public void setStock(Integer stock) {
        this.stock = stock;
    }
}
