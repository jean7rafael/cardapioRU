const functions = require("firebase-functions");
const {Nuxt} = require("nuxt-start");
const express = require("express");
const {spawn} = require("child_process");

const app = express();

// Configurar Nuxt.js
const isDev = process.env.NODE_ENV !== "production";
const nuxtConfig = require("./nuxt.config.js");
nuxtConfig.dev = isDev;
const nuxt = new Nuxt(nuxtConfig);

// Middleware para Nuxt.js
app.use(nuxt.render);

// Rota para o Flask
app.get("/cardapio", (req, res) => {
  const process = spawn("python3", ["main.py"]);
  process.stdout.on("data", (data) => {
    res.send(data.toString());
  });
  process.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
    res.status(500).send(data.toString());
  });
});

exports.api = functions.https.onRequest(app);
