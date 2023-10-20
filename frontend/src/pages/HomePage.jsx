import { useEffect, useRef } from "react";
import MovieCard from '../components/MovieCard';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const HomePage = ({isLoading, setLoading, movies, searchMovies, rates}) => {

    useEffect(() => {
    }, [isLoading, movies])

    if(isLoading) {
        return(
            <div>LOADING</div>
        )
    }
    else{
        return(
            <div>
                <Navbar setLoading={setLoading} searchMovies={searchMovies}/>
                <div style={{display: "flex", justifyContent: "center"}}>
                    <div style={{display: "flex", flexWrap: "wrap", justifyContent: "start", marginLeft: "5%", marginRight: "5%"}}>
                        <MovieCard id={299536} rates={rates} recommended={false} />
                        <MovieCard id={299536} rates={rates} recommended={false} />
                        <MovieCard id={299536} rates={rates} recommended={false} />
                        <MovieCard id={299536} rates={rates} recommended={false} />
                        <MovieCard id={299536} rates={rates} recommended={false} />
                        <MovieCard id={299536} rates={rates} recommended={false} />
                        <MovieCard id={299536} rates={rates} recommended={false} />
                        <MovieCard id={299536} rates={rates} recommended={false} />
                    </div>
                </div>
                <Footer rates={rates} setLoading={setLoading} movies={movies} />
            </div>
        )
    }
}

export default HomePage;