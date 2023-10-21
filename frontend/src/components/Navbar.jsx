import { useState } from "react";
import { searchQuery } from '../Api.js';
import { useNavigate } from "react-router";

const Navbar = ({setLoading, searchMovies}) => {
    const [query, setQuery] = useState("");
    const navigate = useNavigate();

    const search = async (query) => {
        navigate("/search");
        setLoading(true);
        const results = await searchQuery(query);
        searchMovies.current = results;
        setLoading(false);
    }
    
    return(
        <header>
            <div className="container-logo">
                <button onClick={() => {navigate("/")}} className="home_btn"><img src="https://img.icons8.com/ios/50/000000/home--v1.png"/></button>
            </div>           
            <div className="container-search">
                <input type="text" placeholder="Search" id="search" 
                className="search" 
                onChange={(event) => {
                    setQuery(event.target.value);}} 
                onKeyDown={(event) => {
                    if(event.key === "13" || event.key === "Enter"){
                        search(query);
                    }}}/>
            </div>
        </header>
    )
}

export default Navbar;