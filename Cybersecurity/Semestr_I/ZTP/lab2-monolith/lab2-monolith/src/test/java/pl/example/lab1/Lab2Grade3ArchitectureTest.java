package pl.example.lab1;

import org.junit.jupiter.api.Test;
import pl.example.lab1.controller.ShopController;
import pl.example.lab1.store.InMemoryStore;

import java.lang.reflect.Field;

import static org.junit.jupiter.api.Assertions.*;

class Lab2Grade3ArchitectureTest {

    @Test
    void controllerShouldNotDependOnInMemoryStore() {
        Field[] fields = ShopController.class.getDeclaredFields();
        for (Field f : fields) {
            assertNotEquals(InMemoryStore.class, f.getType(),
                    "ShopController must not depend directly on InMemoryStore (use ShopService)");
        }
    }

    @Test
    void serviceLayerShouldExist() throws Exception {
        Class.forName("pl.example.lab1.service.ShopService");
        Class.forName("pl.example.lab1.service.ShopServiceImpl");
    }

    @Test
    void dtoClassesShouldExist() throws Exception {
        Class.forName("pl.example.lab1.dto.ProductCreateRequest");
        Class.forName("pl.example.lab1.dto.OrderCreateRequest");
    }
}
