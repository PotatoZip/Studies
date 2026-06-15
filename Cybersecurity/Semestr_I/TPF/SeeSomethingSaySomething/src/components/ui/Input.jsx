function Input({ label, error, className = '', ...props }) {
  return (
    <div className={`w-full ${className}`}>
      {label && <label className="block text-sm font-bold text-slate-600 mb-1">{label}</label>}
      <input 
        className="w-full border border-slate-300 rounded-lg px-4 py-2 focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all placeholder:text-slate-400"
        {...props}
      />
      {error && <span className="text-xs text-error mt-1">{error}</span>}
    </div>
  );
}

export default Input;