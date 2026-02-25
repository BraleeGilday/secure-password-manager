import { Link } from "react-router-dom";

function FormLink({ to, children }) {
  return (
    <Link to={to} className="form-link">
      {children}
    </Link>
  );
}

export default FormLink;
