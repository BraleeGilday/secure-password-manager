import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

export default function Searchbar() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initial = (searchParams.get("search") || "").toString();
  const [searchValue, setSearchValue] = useState(initial);

  // Keep input current if navigation updates query
  useEffect(() => {
    const next = (searchParams.get("search") || "").toString();
    setSearchValue(next);
  }, [searchParams]);

  const handleUserInput = (e) => {
    const val = e.target.value;
    setSearchValue(val);

    const nextParams = new URLSearchParams(searchParams);
    if (val.trim()) {
      nextParams.set("search", val);
    } else {
      nextParams.delete("search");
    }
    setSearchParams(nextParams, { replace: true });
  };

  return (
    <div className="searchbar">
      <input
        id="search"
        className="searchbar"
        type="text"
        placeholder="Search by site..."
        onChange={handleUserInput}
        value={searchValue}
      />
    </div>
  );
}