import { useEffect } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import MovieCard from '../components/MovieCard';
import Loading from '../components/Loading';

const SearchPage = ({isLoading, setLoading, searchMovies, rates, movies}) => {

    useEffect(() => {
    }, [isLoading, searchMovies])

    return(
        isLoading ? <Loading /> :
        <div>
            <Navbar setLoading={setLoading} searchMovies={searchMovies} />
            <div style={{display: "flex", flexWrap: "wrap", justifyContent: "start", marginLeft: "5%", marginRight: "5%"}}>
                {searchMovies && searchMovies.current.map((id, key) => (
                    <MovieCard rates={rates} id={id} key={key} recommended={false} />
                ))}
            </div>
            <Footer rates={rates} setLoading={setLoading} movies={movies}/>
        </div>
    )
}

export default SearchPage;