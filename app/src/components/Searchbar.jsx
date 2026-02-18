import {useState} from 'react';
export default function Searchbar() {
    const getToken = () => localStorage.getItem('token');
    const [searchValue, setSearchValue] = useState("");
    const handleUserInput = (e) => {
        setSearchValue(e.target.value);
    }

    return (
        <>
        <div className='searchbar'>
            <input 
                id="search"
                className='searchbar'
                type="text"
                placeholder='Search passwords...'
                onChange={handleUserInput}
                value={searchValue}
            />
        </div>
        </>
    )
}