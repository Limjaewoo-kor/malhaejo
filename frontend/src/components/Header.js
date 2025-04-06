import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { ThemeContext } from '../contexts/ThemeContext';
import { Moon, Sun } from 'lucide-react'; // 아이콘용

function Header() {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <header className="flex justify-between items-center px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 shadow-sm">
      <div>
        <h1 className="text-xl font-bold text-blue-600 dark:text-blue-300">말해조 🗣️</h1>
        <nav className="mt-1 space-x-4 text-sm text-gray-700 dark:text-gray-300">
          <Link to="/">홈</Link>
          <Link to="/history">히스토리</Link>
          <Link to="/templates">템플릿</Link>
          <Link to="/feedback">피드백</Link>
        </nav>
      </div>

      <button
        onClick={toggleTheme}
        className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 hover:scale-105 transition-transform"
        title="테마 전환"
      >
        {theme === 'dark' ? <Sun className="w-5 h-5 text-yellow-300" /> : <Moon className="w-5 h-5 text-gray-800" />}
      </button>
    </header>
  );
}

export default Header;
