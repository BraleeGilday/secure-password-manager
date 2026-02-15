import { Link } from 'react-router-dom';

export default function CredentialRow({ id, site }) {
  return (
    <Link className="cred-row" to={`/credentials/${id}`} title={site}>
      <span>{site}</span>
      <span aria-hidden="true">▾</span>
    </Link>
  );
}
