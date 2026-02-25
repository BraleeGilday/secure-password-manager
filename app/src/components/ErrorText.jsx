function ErrorText({ children }) {
  if (!children) return null;

  return <p className="error-text">{children}</p>;
}

export default ErrorText;