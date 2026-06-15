function Card({ children, className = '', ...props }) {
  return (
    <div className={`bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden ${className}`} {...props}>
      {children}
    </div>
  );
}

export default Card;