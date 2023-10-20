import './App.css';
import './styles.css';
import 'primeicons/primeicons.css';
import { Routes, Route } from "react-router-dom";
import { useState, useRef } from "react";
import HomePage from './pages/HomePage';
import MoviePage from './pages/MoviePage';
import SearchPage from './pages/SearchPage';

function App() {
  const [isLoading, setLoading] = useState(false);
  const movies = useRef([]);
  const searchMovies = useRef([]);
  const rates = useRef([]);

  return (
    <>
      <Routes>
        <Route exact path="/" element={<HomePage isLoading={isLoading} setLoading={setLoading} movies={movies} searchMovies={searchMovies} rates={rates} />}/>
        <Route exact path="/movies" element={<MoviePage isLoading={isLoading} setLoading={setLoading} movies={movies} searchMovies={searchMovies} />}/>
        <Route exact path="/search" element={<SearchPage isLoading={isLoading} setLoading={setLoading} searchMovies={searchMovies} rates={rates} movies={movies} />}/>
      </Routes>
    </>
  );
}

export default App;
