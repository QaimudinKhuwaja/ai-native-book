import React from 'react';
import {useThemeConfig, useColorMode} from '@docusaurus/theme-common';
import {
  splitNavbarItems,
  useNavbarConfig,
  useNavbarMobileSidebar,
} from '@docusaurus/theme-common/internal';
import NavbarItem from '@theme/NavbarItem';
import NavbarColorModeToggle from '@theme/Navbar/ColorModeToggle';
import SearchBar from '@theme/SearchBar';
import NavbarMobileSidebarToggle from '@theme/Navbar/MobileSidebar/Toggle';
import NavbarLogo from '@theme/Navbar/Logo';
import NavbarSearch from '@theme/Navbar/Search';

import styles from './index.module.css';

function Navbar(): JSX.Element {
  const {
    navbar: {hideOnScroll, style},
  } = useThemeConfig();
  const {colorMode, setColorMode} = useColorMode();
  const {navbarHook, navbarCustom, style: navbarStyle} = useNavbarConfig();

  const [leftItems, rightItems] = splitNavbarItems(navbarHook.items);

  const mobileSidebar = useNavbarMobileSidebar();

  // Custom Theme Toggle
  const toggleTheme = () => {
    setColorMode(colorMode === 'dark' ? 'light' : 'dark');
  };

  return (
    <nav
      className={styles.navbar}
      style={{
        backgroundColor: navbarStyle?.backgroundColor || 'var(--ifm-navbar-background-color)',
      }}>
      <div className={styles.navbarInner}>
        <NavbarMobileSidebarToggle />
        <NavbarLogo />
        <ul className={styles.navbarItems}>
          {leftItems.map((item, i) => (
            <NavbarItem {...item} key={i} />
          ))}
        </ul>
        <ul className={styles.navbarItems}>
          {rightItems.map((item, i) => (
            <NavbarItem {...item} key={i} />
          ))}
          {/* Custom Theme Toggle Button */}
          <li className="navbar__item">
            <button
              className="button button--secondary button--sm"
              onClick={toggleTheme}
              aria-label={`Switch between ${colorMode === 'dark' ? 'light' : 'dark'} mode`}>
              {colorMode === 'dark' ? '☀️' : '🌙'}
            </button>
          </li>
          <NavbarSearch />
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;