package pl.example.lab8;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class Grade4QueryAndPagingTest {

  @Autowired
  MockMvc mvc;

  @Test
  @DisplayName("4.0 /products/search supports paging+sorting via Spring Data")
  void searchProductsPagedSorted() throws Exception {
    mvc.perform(post("/products").contentType(MediaType.APPLICATION_JSON)
        .content("{\"name\":\"AAA\",\"price\":50.00,\"stock\":1}")).andExpect(status().isCreated());
    mvc.perform(post("/products").contentType(MediaType.APPLICATION_JSON)
        .content("{\"name\":\"AAB\",\"price\":10.00,\"stock\":1}")).andExpect(status().isCreated());
    mvc.perform(post("/products").contentType(MediaType.APPLICATION_JSON)
        .content("{\"name\":\"BBB\",\"price\":20.00,\"stock\":1}")).andExpect(status().isCreated());

    mvc.perform(get("/products/search")
            .param("q", "aa")
            .param("minPrice", "0.00")
            .param("maxPrice", "100.00")
            .param("page", "0")
            .param("size", "1")
            .param("sort", "price,asc"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.content.length()").value(1))
        .andExpect(jsonPath("$.content[0].name").value("AAB"))
        .andExpect(jsonPath("$.totalElements").value(2));

    mvc.perform(get("/products/search")
            .param("q", "aa")
            .param("minPrice", "0.00")
            .param("maxPrice", "100.00")
            .param("page", "1")
            .param("size", "1")
            .param("sort", "price,asc"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.content.length()").value(1))
        .andExpect(jsonPath("$.content[0].name").value("AAA"));
  }

  @Test
  @DisplayName("4.0 /orders supports paging+sorting by createdAt desc")
  void ordersPagedSorted() throws Exception {
    mvc.perform(post("/products").contentType(MediaType.APPLICATION_JSON)
        .content("{\"name\":\"P\",\"price\":10.00,\"stock\":10}")).andExpect(status().isCreated());

    mvc.perform(post("/orders").contentType(MediaType.APPLICATION_JSON)
        .content("{\"productId\":1,\"quantity\":1}")).andExpect(status().isCreated());
    mvc.perform(post("/orders").contentType(MediaType.APPLICATION_JSON)
        .content("{\"productId\":1,\"quantity\":2}")).andExpect(status().isCreated());

    mvc.perform(get("/orders")
            .param("page", "0")
            .param("size", "1")
            .param("sort", "createdAt,desc"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.content.length()").value(1))
        .andExpect(jsonPath("$.content[0].quantity").value(2))
        .andExpect(jsonPath("$.totalElements").value(2));
  }
}
