import CreateGame from "./pages/CreateGame";
import Game from "./pages/Game";
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<CreateGame />} />
                <Route path="/games/:gameId" element={<Game />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;