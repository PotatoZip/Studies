package pl.example.lab6.controller;

import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import pl.example.lab6.dto.BookForm;
import pl.example.lab6.service.LibraryService;

@Controller
public class BooksController {

    private final LibraryService libraryService;

    public BooksController(LibraryService libraryService) {
        this.libraryService = libraryService;
    }

    @GetMapping("/books")
    public String books(Model model) {
        model.addAttribute("books", libraryService.getBooks());
        return "books/list";
    }

    @GetMapping("/books/new")
    public String newBookForm(Model model) {
        if (!model.containsAttribute("bookForm")) {
            model.addAttribute("bookForm", new BookForm());
        }
        return "books/form";
    }

    @PostMapping("/books")
    public String createBook(@Valid @ModelAttribute("bookForm") BookForm bookForm,
            BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            return "books/form";
        }
        libraryService.createBook(bookForm);
        return "redirect:/books";
    }
}
