import { forwardRef } from 'react';

const Button = forwardRef(({ children, variant = 'primary', size = 'md', className = '', type = 'button', ...props }, ref) => {
  const baseStyle = "inline-flex items-center justify-center gap-2 rounded-full font-bold transition-all focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";
  
  const variants = {
    primary: "bg-primary text-on-primary shadow-sm hover:shadow-md hover:bg-primary/90 hover:-translate-y-0.5 active:translate-y-0",
    secondary: "bg-secondary-fixed text-on-secondary-fixed hover:bg-[#ffe5bc] hover:-translate-y-0.5 active:translate-y-0",
    outline: "border border-outline-variant bg-white text-primary hover:bg-slate-50 hover:-translate-y-0.5 active:translate-y-0",
    danger: "bg-error text-white hover:bg-error/90 hover:-translate-y-0.5 active:translate-y-0",
    ghost: "bg-transparent text-slate-600 hover:bg-slate-100 hover:text-slate-900"
  };

  const sizes = {
    sm: "px-4 py-1.5 text-sm",
    md: "px-5 py-2.5 text-base",
    lg: "px-8 py-3 text-lg"
  };

  const selectedVariant = variants[variant] || variants.primary;
  const selectedSize = sizes[size] || sizes.md;

  return (
    <button type={type} ref={ref} className={`${baseStyle} ${selectedSize} ${selectedVariant} ${className}`} {...props}>
      {children}
    </button>
  );
});

Button.displayName = 'Button';

export default Button;