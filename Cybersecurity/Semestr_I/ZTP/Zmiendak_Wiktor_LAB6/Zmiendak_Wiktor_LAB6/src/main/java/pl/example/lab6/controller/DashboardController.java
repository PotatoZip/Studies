package pl.example.lab6.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import pl.example.lab6.service.LibraryService;

@Controller
public class DashboardController {

    private final LibraryService libraryService;

    public DashboardController(LibraryService libraryService) {
        this.libraryService = libraryService;
    }

    @GetMapping({ "/", "/dashboard" })
    public String dashboard(Model model) {
        model.addAttribute("dashboard", libraryService.getDashboard());
        return "dashboard";
    }
}
