const menu = document.querySelector(".menu"),
  links = document.querySelector(".nav-links");
if (menu && links) {
  menu.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
  });
  links
    .querySelectorAll("a")
    .forEach((a) =>
      a.addEventListener("click", () => links.classList.remove("open")),
    );
}

if (links) {
  const normalizePath = (value) => {
    const path = value.replace(/\/index\.html$/, "/");
    return path.length > 1 ? path.replace(/\/$/, "") : path;
  };
  const updateActiveLink = () => {
    const currentPath = normalizePath(window.location.pathname);
    links.querySelectorAll("a").forEach((link) => {
      const url = new URL(link.href, window.location.href);
      const linkPath = normalizePath(url.pathname);
      const isLocation = url.hash === "#ubicacion";
      const isSection =
        linkPath !== "/" && currentPath.startsWith(`${linkPath}/`);
      const selected = isLocation
        ? window.location.hash === "#ubicacion"
        : !window.location.hash && (linkPath === currentPath || isSection);
      link.classList.toggle("active", selected);
      if (selected) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  };
  updateActiveLink();
  window.addEventListener("hashchange", updateActiveLink);
  links.querySelectorAll("a").forEach((link) =>
    link.addEventListener("click", () => {
      links.querySelectorAll("a").forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
    }),
  );
}
document
  .querySelectorAll("[data-year]")
  .forEach((el) => (el.textContent = new Date().getFullYear()));

const whatsappForm = document.querySelector("[data-whatsapp-form]");
if (whatsappForm) {
  whatsappForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!whatsappForm.reportValidity()) return;

    const data = new FormData(whatsappForm);
    const value = (name) => String(data.get(name) || "").trim();
    const lines = [
      "Hola Toyo Services. Quiero solicitar atención para mi Toyota.",
      "",
      `Nombre: ${value("nombre")}`,
      `Modelo: ${value("modelo")}`,
      `Año: ${value("anio") || "No indicado"}`,
      `Servicio: ${value("servicio")}`,
      `Detalle: ${value("mensaje")}`,
      "",
      "Enviado desde toyoservicescartagena.com",
    ];
    const url = `https://wa.me/573018638164?text=${encodeURIComponent(lines.join("\n"))}`;
    window.location.assign(url);
  });
}
