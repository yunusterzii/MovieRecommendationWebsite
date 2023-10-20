import { useEffect, useState } from "react";
import { Rating } from "primereact/rating";
import axios from "axios";

const MovieCard = ({id, rates, recommended}) => {
    const api_key = "8151741cef380652f287f81ee920821d";
    const [found, setFound] = useState(false);
    const [movie, setMovie] = useState({});
    const [rate, setRate] = useState(0);
    const [rateDisabled, setRateDisabled] = useState(false);

    useEffect(() => {
        axios.get("https://api.themoviedb.org/3/movie/" + id + "?api_key=" + api_key)
            .then((response) => {
                setMovie(response.data);
                console.log(response.data);
                setFound(true);
            })
            .catch((error) => {
                console.log(error);
                setFound(false);
            });

        console.log(movie);
    }, [id, recommended])

    const click = () => {
        rates.current = [...rates.current, {movieID: id, value: rate / 2}];
        setRateDisabled(true);
    }

    if(found && movie) {
        return(
            <div className="movie">
                <img src={"https://www.themoviedb.org/t/p/w600_and_h900_bestv2/" + movie.poster_path} alt={movie.title} />
                <div className="movie-info">
                    <div className="title-and-rating">
                        <div style={{width: "60%", height: "3rem", lineHeight: "1.25rem"}} >{movie.title}</div>
                        <div style={{height: "3rem", color: movie.vote_average >= 8 ? "green" : (movie.vote_average >= 5 ? "orange" : "red")}}><i className="pi pi-star-fill" style={{color:"rgb(245, 197, 24)", marginRight:"0.5rem"}} ></i>{movie.vote_average.toFixed(1)}</div>
                    </div>
                    <div className="moreinfo-and-trailer">
                        <div>{movie.release_date.split("-")[0]}</div>
                        <div>{movie.runtime + " mins"}</div>
                        <div><a style={{textDecoration: "none"}} alt="imdb" target="_blank" src="https://img.icons8.com/color/48/imdb.png" href={"https://www.imdb.com/title/" + movie.imdb_id}><img src="https://img.icons8.com/color/48/imdb.png" alt="imdb" style={{fontSize: '1.75rem', color: "white"}}></img></a></div>
                    </div>
                    {!recommended && <div className="rating">
                        <Rating value={rate} visibleOnly disabled={rateDisabled} onChange={(e) => {setRate(e.value); console.log(e.value)}} cancel={false} stars={10} />
                    </div>}
                    {!recommended && <div className="mini-button-div">
                        {!recommended && !rateDisabled && <button className="rate-button" onClick={click} disabled={rate === 0}>Rate</button>}
                    </div>}
                </div>
            </div>
        );
    }
}

export default MovieCard;