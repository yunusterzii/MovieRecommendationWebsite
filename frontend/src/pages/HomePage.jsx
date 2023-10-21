import { useEffect } from "react";
import { getMovies } from '../Api.js';
import MovieCard from '../components/MovieCard';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import Loading from '../components/Loading';

const HomePage = ({isLoading, setLoading, movies, searchMovies, rates, randomMovies, setRandomMovies}) => {

    useEffect(() => {
        if(randomMovies == null) {
            getRandomMovies();
        }
    }, [])

    const getRandomMovies = async () => {
        setLoading(true);
        const data = await getMovies();
        setRandomMovies(data);
        setLoading(false);
    }

    return(
        isLoading ? <Loading /> : 
        <div>
            <Navbar setLoading={setLoading} searchMovies={searchMovies}/>
            <div style={{display: "flex", justifyContent: "center"}}>
                <div style={{display: "flex", flexWrap: "wrap", justifyContent: "start", marginLeft: "5%", marginRight: "5%"}}>
                    {randomMovies?.map((id, key) => (
                        <MovieCard id={id} key={key} rates={rates} recommended={false} />
                    ))}
                </div>
            </div>
            <Footer rates={rates} setLoading={setLoading} movies={movies} />
        </div>
    )
}

export default HomePage;