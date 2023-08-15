import { mode } from '@chakra-ui/theme-tools';

export const globalStyles = {
  colors: {
    brand: {
      500: '#2E86AB', // Custom brand color
      600: '#1F4662', // Darker shade of the brand color
    },
    dark: {
      50: '#F7FAFC', // Light gray for dark mode
      100: '#EDF2F7', // Lighter gray for dark mode
      200: '#E2E8F0', // Medium gray for dark mode
      300: '#CBD5E0', // Gray for dark mode
      400: '#A0AEC0', // Dark gray for dark mode
      500: '#718096', // Darker gray for dark mode
      600: '#4A5568', // Even darker gray for dark mode
      700: '#2D3748', // Darkest gray for dark mode
      800: '#1A202C', // Almost black for dark mode
      900: '#171923', // True black for dark mode
    },
  },
  styles: {
    global: (props) => ({
      body: {
        bg: mode('white', 'dark.800')(props), // White background for light mode, dark background for dark mode
        color: mode('gray.800', 'white')(props), // Dark gray text for light mode, white text for dark mode
        fontFamily: "'Roboto', sans-serif",
        lineHeight: '1.6',
      },
      html: {
        fontFamily: "'Roboto', sans-serif",
      },
      'h1, h2, h3, h4, h5, h6': {
        color: mode('gray.800', 'white')(props), // Dark gray text for light mode, white text for dark mode
        fontWeight: 'bold',
      },
      a: {
        color: mode('brand.500', 'brand.600')(props), // Custom brand color for light mode, darker shade for dark mode
        _hover: {
          textDecoration: 'underline',
        },
      },
      // Customize other elements as needed
      // For example, buttons, cards, input fields, etc.
    }),
  },
};
