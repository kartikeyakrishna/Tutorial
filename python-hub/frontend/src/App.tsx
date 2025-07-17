import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Health from './pages/Health';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Health />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App; 