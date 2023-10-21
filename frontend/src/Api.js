import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/"
});

const submitRates = async (data) => {
    let result = "";
    await api.post("/submitRates/", {
        data
    })
    .then((response) => {
        console.log("SubmitRates - status code " + response.status);
        result = response.data;
    })
    .catch((error) => {
        console.log(error);
    });
    return result;
}

const searchQuery = async (query) => {
    let result = "";
    await api.post("/searchQuery/", {
        query
    })
    .then((response) => {
        console.log("searchQuery - status code " + response.status);
        result = response.data;
    })
    .catch((error) => {
        console.log(error);
    });
    return result;
}

const getMovies = async () => {
    let result = "";
    await api.get("/getMovies/")
    .then((response) => {
        console.log("getMovies - status code " + response.status);
        result = response.data;
    })
    .catch((error) => {
        console.log(error);
    });
    return result;
}

export { submitRates, searchQuery, getMovies};