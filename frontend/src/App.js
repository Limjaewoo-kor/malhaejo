import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import ReactGA from 'react-ga4';
import { UserInputProvider } from './contexts/UserInputContext';
import { ThemeProvider } from './contexts/ThemeContext';
import HomePage from './pages/HomePage';
import PurposePage from './pages/PurposePage';
import InputPage from './pages/InputPage';
import TonePage from './pages/TonePage';
import ResultPage from './pages/ResultPage';
import HistoryPage from './pages/HistoryPage';
import Header from './components/Header';
import TemplatePage from './pages/TemplatePage';
import FeedbackPage from './pages/FeedbackPage';
import NotFoundPage from './pages/NotFoundPage';

// ✅ 페이지 이동 시 GA 이벤트 전송
function usePageTracking() {
  const location = useLocation();

  useEffect(() => {
    ReactGA.send({ hitType: 'pageview', page: location.pathname });
  }, [location]);
}

function AppWrapper() {
  usePageTracking(); // ❗ 함수 안에서 호출

  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/purpose" element={<PurposePage />} />
        <Route path="/input" element={<InputPage />} />
        <Route path="/tone" element={<TonePage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/templates" element={<TemplatePage />} />
        <Route path="/feedback" element={<FeedbackPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <ThemeProvider>
      <UserInputProvider>
        <Router>
          <AppWrapper />
        </Router>
      </UserInputProvider>
    </ThemeProvider>
  );
}

export default App;
