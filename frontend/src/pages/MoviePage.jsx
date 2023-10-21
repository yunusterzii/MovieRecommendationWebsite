import { useEffect } from "react";
import Navbar from "../components/Navbar";
import MovieCard from '../components/MovieCard';

const MoviePage = ({isLoading, setLoading, movies, searchMovies}) => {

    useEffect(() => {
    }, [isLoading, movies])

    if(isLoading) {
        return(
            <div>
                <Navbar setLoading={setLoading} searchMovies={searchMovies} />
                <div>LOADING</div>
            </div>
        )
    }
    else{
        return(
            <div>
                <Navbar setLoading={setLoading} searchMovies={searchMovies} />
                <div style={{display: "flex", flexWrap: "wrap", justifyContent: "start", marginLeft: "5%", marginRight: "5%"}}>
                    {movies.current.map((id, key) => (
                        <MovieCard id={id} key={key} recommended={true} />
                    ))}
                </div>
            </div>
        )
    }
}

export default MoviePage;