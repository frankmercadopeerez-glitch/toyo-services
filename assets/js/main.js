document.documentElement.classList.add("js");
const menu = document.querySelector(".menu"),
  links = document.querySelector(".nav-links");
if (menu && links) {
  menu.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
    menu.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  });
  links
    .querySelectorAll("a")
    .forEach((a) =>
      a.addEventListener("click", () => {
        links.classList.remove("open");
        menu.setAttribute("aria-expanded", "false");
        menu.setAttribute("aria-label", "Abrir menú");
      }),
    );
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && links.classList.contains("open")) {
      links.classList.remove("open");
      menu.setAttribute("aria-expanded", "false");
        menu.setAttribute("aria-label", "Abrir menú");
      menu.focus();
    }
  });
}

if (links) {
  const normalizePath = (value) => {
    const path = value.replace(/\/index\.html$/, "/");
    return path.length > 1 ? path.replace(/\/$/, "") : path;
  };
  const updateActiveLink = () => {
    const currentPath = normalizePath(window.location.pathname);
    const matching = [...links.querySelectorAll("a")].map(link => normalizePath(new URL(link.href).pathname)).filter(path => currentPath === path || (path !== "/" && currentPath.startsWith(`${path}/`)));
    const closest = matching.sort((a,b) => b.length-a.length)[0];
    links.querySelectorAll("a").forEach((link) => {
      const url = new URL(link.href, window.location.href);
      const linkPath = normalizePath(url.pathname);
      const isLocation = url.hash === "#ubicacion";
      const isSection =
        linkPath !== "/" && currentPath.startsWith(`${linkPath}/`);
      const atLocation = currentPath === "/" && window.location.hash === "#ubicacion";
      const selected = isLocation
        ? atLocation
        : !atLocation && linkPath === closest && (linkPath === currentPath || isSection);
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
  const service = whatsappForm.elements.servicio;
  const parts = whatsappForm.querySelector("[data-parts-fields]");
  const hint = whatsappForm.querySelector("[data-service-hint]");
  const preview = whatsappForm.querySelector("[data-request-preview]");
  const message = whatsappForm.querySelector("#request-message");
  const send = whatsappForm.querySelector("[data-request-link]");
  const status = whatsappForm.querySelector("[data-copy-status]");
  const params = new URLSearchParams(location.search);
  const requestedService = params.get("servicio");
  if ([...service.options].some(o => o.value === requestedService)) service.value = requestedService;
  const allowedModels = [...whatsappForm.querySelectorAll("datalist option")].map(o => o.value);
  if (allowedModels.includes(params.get("modelo"))) whatsappForm.elements.modelo.value = params.get("modelo");
  whatsappForm.elements.anio.max = String(new Date().getFullYear() + 1);
  const hints = {
    repuestos: "Indica la pieza, lado o posición. Adjunta la foto y el VIN después, en el chat de WhatsApp.",
    "mantenimiento-general": "Cuéntanos cuándo fue el último servicio y qué se realizó, si lo recuerdas.",
    "aceite-filtros": "Indica el último cambio, kilometraje y motor. Confirmaremos la especificación aplicable.",
    "diagnostico-electronico": "Describe el testigo o síntoma, cuándo aparece y si ocurre en frío o en caliente.",
    transmision: "Indica si la caja es automática o mecánica y en qué condición aparece el síntoma.",
    "aire-acondicionado": "Cuéntanos si pierde frío siempre, al detenerte o después de conducir.",
    "frenos-suspension": "Indica si el ruido o vibración aparece al frenar, girar o pasar un desnivel."
  };
  const updateService = () => {
    parts.hidden = service.value !== "repuestos";
    parts.disabled = parts.hidden;
    hint.textContent = hints[service.value] || "Describe lo que ocurre o el trabajo que deseas realizar. No necesitas conocer la causa.";
  };
  service.addEventListener("change", updateService);
  updateService();
  whatsappForm.hidden = false;
  whatsappForm.addEventListener("input", event => {
    if (event.target.matches("input, textarea") && !event.target.readOnly) event.target.setCustomValidity("");
    preview.hidden = true;
    send.removeAttribute("href");
  });
  whatsappForm.addEventListener("change", () => { preview.hidden = true; send.removeAttribute("href"); });
  whatsappForm.addEventListener("submit", event => {
    event.preventDefault();
    for (const field of [whatsappForm.elements.modelo, whatsappForm.elements.mensaje]) {
      field.setCustomValidity(field.value.trim() ? "" : "Escribe información; los espacios solos no son válidos.");
    }
    if (!whatsappForm.reportValidity()) return;
    const data = new FormData(whatsappForm);
    const value = name => String(data.get(name) || "").trim();
    const lines = ["Hola Toyo Services. Quiero solicitar atención para mi Toyota.", ""];
    for (const [name,label] of [["nombre","Nombre"],["modelo","Modelo"],["anio","Año"],["kilometraje","Kilometraje"],["version","Motor o versión"]]) {
      if(value(name)) lines.push(`${label}: ${value(name)}${name === "kilometraje" ? " km" : ""}`);
    }
    lines.push(`Servicio: ${service.selectedOptions[0].textContent}`);
    if(!parts.hidden) for(const [name,label] of [["referencia","Pieza o referencia"],["instalacion","Instalación"]]) {
      if(value(name)) lines.push(`${label}: ${value(name)}`);
    }
    lines.push(`Detalle: ${value("mensaje")}`, "", "Solicitud preparada en toyoservicescartagena.com");
    message.value = lines.join("\n");
    send.href = `https://wa.me/573018638164?text=${encodeURIComponent(message.value)}`;
    status.textContent = "La solicitud aún no se ha enviado. Revísala y continúa en WhatsApp.";
    preview.hidden = false;
    whatsappForm.querySelector("[data-preview-heading]").focus();
  });
  whatsappForm.querySelector("[data-copy-request]").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(message.value);
      status.textContent = "Mensaje copiado. Pégalo en el chat de Toyo Services: +57 301 863 8164.";
    } catch {
      message.focus(); message.select();
      status.textContent = "Seleccionamos el mensaje para que puedas copiarlo manualmente.";
    }
  });
}

// Progressive enhancement: every guide remains crawlable without JavaScript.
const guideSearch = document.querySelector("[data-guide-search]");
if (guideSearch) {
  const input = guideSearch.querySelector("input");
  const status = guideSearch.querySelector("[data-guide-count]");
  const sections = [...document.querySelectorAll(".guide-topic")];
  const normalize = (text) => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const filterGuides = () => {
    const terms = normalize(input.value.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    for (const section of sections) {
      let visible = 0;
      for (const item of section.querySelectorAll("li")) {
        item.hidden = !terms.every((term) => normalize(item.textContent).includes(term));
        if (!item.hidden) visible++;
      }
      section.hidden = visible === 0;
      count += visible;
    }
    status.textContent = count ? `${count} ${count === 1 ? "guía disponible" : "guías disponibles"}` : "No encontramos esa búsqueda. Prueba con el modelo o con otro síntoma.";
  };
  input.addEventListener("input", filterGuides);
  document.querySelectorAll(".topic-links a").forEach((link) => link.addEventListener("click", () => {
    input.value = "";
    filterGuides();
  }));
  guideSearch.hidden = false;
  filterGuides();
}

// Search the actual service descriptions, with common customer vocabulary.
const serviceSearch = document.querySelector("[data-service-search]");
if (serviceSearch) {
  const input = serviceSearch.querySelector("input");
  const rows = [...document.querySelectorAll(".service-row")];
  const norm = text => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const aliases = {
    transmision: "caja cambios tirones embrague clutch",
    frenos: "ruido vibracion pastillas discos amortiguadores bujes rotulas",
    diagnostico: "check engine testigo luz bateria electrico sensor no enciende arranque",
    motor: "recalienta temperatura fuga radiador termostato bomba agua",
    "mecanica-avanzada": "aire acondicionado no enfria compresor falla potencia",
    aceite: "lubricante filtro cambio aceite",
    repuestos: "pieza referencia vin original oem alternativo",
    estetica: "actualizacion estetica interior luces faros"
  };
  const filter = () => {
    const terms = norm(input.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    rows.forEach(row => {
      const text = norm(row.textContent + " " + (aliases[row.id] || ""));
      row.hidden = !terms.every(term => text.includes(term));
      if (!row.hidden) count++;
    });
    serviceSearch.querySelector("[data-service-count]").textContent = `${count} ${count === 1 ? "servicio disponible para consultar" : "servicios disponibles para consultar"}`;
    serviceSearch.querySelector("[data-service-empty]").hidden = count !== 0;
    document.querySelectorAll(".supplementary-intro").forEach(el => el.hidden = terms.length > 0);
    for (const section of document.querySelectorAll("#service-results, #service-protection-results")) {
      section.hidden = ![...section.querySelectorAll(".service-row")].some(row => !row.hidden);
    }
  };
  input.addEventListener("input", filter);
  serviceSearch.querySelector("[data-clear-services]").addEventListener("click", () => { input.value = ""; filter(); input.focus(); });
  const revealHash = () => {
    const target = document.getElementById(location.hash.slice(1));
    if (target && target.classList.contains("service-row")) { input.value = ""; filter(); target.scrollIntoView(); }
  };
  window.addEventListener("hashchange", revealHash);
  serviceSearch.hidden = false;
  filter();
}
