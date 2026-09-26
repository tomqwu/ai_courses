/*
 * Your catalog. This is the only file you need to edit to change what the page shows.
 *
 * It is plain JavaScript rather than JSON so the page works when you double-click index.html:
 * a browser will not let a page read a separate .json file from your disk, but it will run a
 * script you load with <script src>. Keep the shape below and the page takes care of the rest.
 *
 * Every product needs: id, name, category, price, summary.
 * Optional: image (a path such as "images/mug.jpg"), tags, color (used when there is no image),
 * and buyUrl — a link to a checkout hosted somewhere else. GitHub Pages is a place to show your
 * products, not to sell them: its terms do not allow a site that runs an online shop.
 */
window.CATALOG = {
  store: {
    name: "Harbour Clay Studio",
    tagline: "Small-batch stoneware, thrown and glazed by hand.",
    currency: "USD",
    contact: "mailto:hello@example.com",
    note: "Prices include glazing and firing. Each piece is made to order, so allow two weeks."
  },
  products: [
    {
      id: "everyday-mug",
      name: "Everyday Mug",
      category: "Mugs",
      price: 32,
      summary: "A 350 ml mug with a thumb rest, glazed inside and out in satin oatmeal.",
      tags: ["dishwasher safe", "350 ml"],
      color: "#b9a88f",
      buyUrl: ""
    },
    {
      id: "tall-latte-mug",
      name: "Tall Latte Mug",
      category: "Mugs",
      price: 36,
      summary: "Taller and narrower for layered coffee. Deep ocean glaze that pools blue at the rim.",
      tags: ["450 ml"],
      color: "#3f6f86",
      buyUrl: ""
    },
    {
      id: "serving-bowl",
      name: "Serving Bowl",
      category: "Bowls",
      price: 68,
      summary: "A wide, shallow bowl for salads and shared plates. Speckled white with a raw foot.",
      tags: ["28 cm", "oven safe"],
      color: "#d9d4c7",
      buyUrl: ""
    },
    {
      id: "noodle-bowl",
      name: "Noodle Bowl",
      category: "Bowls",
      price: 42,
      summary: "Deep enough for broth, with a slight flare so the chopsticks rest easily.",
      tags: ["dishwasher safe"],
      color: "#7a5a44",
      buyUrl: ""
    },
    {
      id: "bud-vase",
      name: "Bud Vase",
      category: "Vases",
      price: 28,
      summary: "A single-stem vase with a narrow neck. Every glaze run is different.",
      tags: ["one of a kind"],
      color: "#8a9a6b",
      buyUrl: ""
    },
    {
      id: "gift-set",
      name: "Morning Gift Set",
      category: "Sets",
      price: 95,
      summary: "Two Everyday Mugs and a small plate, boxed. The most-asked-for gift in the studio.",
      tags: ["gift boxed"],
      color: "#c27c52",
      buyUrl: ""
    }
  ]
};
