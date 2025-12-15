/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
    "./app/**/*.{js,jsx}",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        text: {
          gradient: "var(--gradient)",
        },
        bordercolor: "hsl(var(--bordercolor))",
        background: {
          DEFAULT: "hsla(240, 4.3%, 7%)",
        },
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        gray: {
          DEFAULT: "hsl(var(--background))",
          50: "hsl(240, 4.3%, 98.5%)",
          600: "hsl(0, 0%, 50.6%)",
          700: "hsl(240, 4.3%, 20.5%)",
          800: "hsl(240, 4.3%, 13.5%)",
          900: "hsl(240, 4.3%, 7%)",
        },
        foreground: "hsl(var(--foreground))",
        text: {
          gray: "hsla(0, 0%, 51%, 1)",
          DEFAULT: "hsl(var(--text))",
          gradient: "hsl(var(--text-gradient))",
          secondary: "hsl(var(--text-secondary))",
          tertiary: "hsl(var(--text-tertiary))",
          quaternary: "hsl(var(--text-quaternary))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
          background: "hsl(var(--primary-background))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsla(0, 0%, 51%, 1)",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsla(240, 4%, 14%, 1)",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
