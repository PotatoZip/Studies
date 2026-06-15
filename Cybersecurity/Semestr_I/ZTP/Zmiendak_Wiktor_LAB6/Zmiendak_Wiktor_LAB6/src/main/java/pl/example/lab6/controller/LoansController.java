package pl.example.lab6.controller;

import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import pl.example.lab6.dto.LoanForm;
import pl.example.lab6.service.LibraryService;

@Controller
public class LoansController {

    private final LibraryService libraryService;

    public LoansController(LibraryService libraryService) {
        this.libraryService = libraryService;
    }

    @GetMapping("/loans")
    public String loans(@RequestParam(name = "active", defaultValue = "false") boolean active,
            Model model) {
        model.addAttribute("loans", libraryService.getLoans(active));
        model.addAttribute("activeOnly", active);
        return "loans/list";
    }

    @GetMapping("/loans/new")
    public String newLoanForm(@RequestParam("bookId") long bookId, Model model) {
        model.addAttribute("selectedBook", libraryService.getBook(bookId));
        if (!model.containsAttribute("loanForm")) {
            model.addAttribute("loanForm", new LoanForm(bookId, ""));
        }
        return "loans/form";
    }

    @PostMapping("/loans")
    public String createLoan(@Valid @ModelAttribute("loanForm") LoanForm loanForm,
            BindingResult bindingResult,
            Model model) {
        if (bindingResult.hasErrors()) {
            if (loanForm.getBookId() != null) {
                model.addAttribute("selectedBook", libraryService.getBook(loanForm.getBookId()));
            }
            return "loans/form";
        }

        try {
            libraryService.createLoan(loanForm);
            return "redirect:/loans";
        } catch (IllegalStateException ex) {
            bindingResult.reject("loan.unavailable", ex.getMessage());
            model.addAttribute("selectedBook", libraryService.getBook(loanForm.getBookId()));
            return "loans/form";
        }
    }

    @PostMapping("/loans/{loanId}/return")
    public String returnLoan(@PathVariable long loanId) {
        libraryService.returnLoan(loanId);
        return "redirect:/loans";
    }
}
