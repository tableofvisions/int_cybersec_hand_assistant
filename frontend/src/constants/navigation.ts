export const footerLinksAssistant = [
  {
    label: "Kontakt",
    route: "/assistant/contact",
    external: false,
  },
  {
    label: "Impressum",
    route: "/assistant/impressum",
    external: false,
  },
  {
    label: "Datenschutzerklärung",
    route: "/assistant/privacy",
    external: false,
  },
  {
    label: "Nutzungsbedingungen",
    route: "/assistant/terms",
    external: false,
  },
];

export const footerLinksAuth = [
  {
    label: "Projektbeschreibung",
    route: "/auth/projektbeschreibung",
    external: false,
  },
  {
    label: "Kontakt",
    route: "/auth/contact",
    external: false,
  },
  {
    label: "Impressum",
    route: "/auth/impressum",
    external: true,
  },
  {
    label: "Datenschutzerklärung",
    route: "/auth/privacy",
    external: false,
  },
  {
    label: "Nutzungsbedingungen",
    route: "/auth/terms",
    external: false,
  },
];

export const navBarLinks = [
  {
    label: "Übersicht",
    icon: "grid_view",
    route: "/assistant/dashboard",
    spacer: true,
    recommendations: false,
  },
  {
    label: "ITSM-Maßnahmen",
    icon: "account_tree",
    route: "/assistant/measures",
    spacer: true,
    recommendations: true,
  },
  {
    label: "IT-Sicherheitswissen",
    icon: "developer_guide",
    route: "/assistant/glossary",
    spacer: false,
    recommendations: false,
  },
  {
    label: "Einstellungen",
    icon: "tune",
    route: "/assistant/settings",
    spacer: false,
    recommendations: false,
  },
];
