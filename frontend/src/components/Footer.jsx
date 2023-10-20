import { submitRates } from '../Api.js';
import { useNavigate } from "react-router";

const Footer = ({rates, setLoading, movies}) => {
    const navigate = useNavigate();

    const submitClick = async () => {
        navigate("/movies");
        const data = rates.current;
        setLoading(true);
        const movieList = await submitRates(data);
        console.log(movieList);
        movies.current = movieList;
        setLoading(false);
    }

    return(
        <div>
            <div class="submitation">
                <button class="sbmt" onClick={submitClick} type="submit">Submit</button>
            </div>
        </div>
    )
}

export default Footer;