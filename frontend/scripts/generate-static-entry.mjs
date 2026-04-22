import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, "..");
const serverEntryPath = path.join(projectRoot, "dist", "server", "server.js");
const clientDistPath = path.join(projectRoot, "dist", "client");

const serverModule = await import(pathToFileURL(serverEntryPath).href);
const server = serverModule.default;

if (!server || typeof server.fetch !== "function") {
  throw new Error("TanStack server entry did not export a fetch handler.");
}

const response = await server.fetch(new Request("http://localhost/"));
if (!response.ok) {
  throw new Error(`Failed to render static HTML. Status: ${response.status}`);
}

const html = await response.text();
await mkdir(clientDistPath, { recursive: true });
await writeFile(path.join(clientDistPath, "index.html"), html, "utf8");
await writeFile(path.join(clientDistPath, "404.html"), html, "utf8");

console.log("Generated dist/client/index.html and dist/client/404.html");
