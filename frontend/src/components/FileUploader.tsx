"use client";

import { type ChangeEvent, type FormEvent, useState } from "react";

type UploadResponse = {
  filename: string;
  file_extension: string;
  size_bytes: number;
  character_count: number;
  chunk_count: number;
  embedding_count: number;
  embedding_dimension: number;
};

const UPLOAD_URL = "http://127.0.0.1:8000/files/upload";
const SUPPORTED_EXTENSIONS = [".txt", ".md", ".py", ".js", ".csv"];

function getFileExtension(filename: string) {
  const dotIndex = filename.lastIndexOf(".");

  if (dotIndex === -1) {
    return "";
  }

  return filename.slice(dotIndex).toLowerCase();
}

function formatBytes(bytes: number) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  return `${(bytes / 1024).toFixed(1)} KB`;
}

export default function FileUploader() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;

    setSelectedFile(file);
    setUploadResult(null);
    setErrorMessage("");
  }

  async function handleUpload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const form = event.currentTarget;

    if (!selectedFile) {
      setErrorMessage("Please choose a file before uploading.");
      return;
    }

    const fileExtension = getFileExtension(selectedFile.name);

    if (!SUPPORTED_EXTENSIONS.includes(fileExtension)) {
      setErrorMessage("Supported file types: .txt, .md, .py, .js, .csv");
      return;
    }

    setIsUploading(true);
    setErrorMessage("");
    setUploadResult(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(UPLOAD_URL, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "File upload failed.");
      }

      setUploadResult(data as UploadResponse);
      form.reset();
      setSelectedFile(null);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "File upload failed.";

      setErrorMessage(message);
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <section
      aria-label="File upload"
      className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
    >
      <div>
        <p className="text-sm font-semibold text-slate-950">Upload a file</p>
        <p className="mt-1 text-sm leading-6 text-slate-500">
          Send supported files to the FastAPI backend for extraction, chunking,
          local embeddings, and in-memory storage.
        </p>
      </div>

      <form onSubmit={handleUpload} className="mt-5 space-y-4">
        <label className="block rounded-xl border border-dashed border-slate-300 bg-slate-50 p-4">
          <span className="block text-sm font-medium text-slate-700">
            Choose a supported file
          </span>
          <span className="mt-1 block text-xs text-slate-500">
            .txt, .md, .py, .js, .csv
          </span>
          <input
            type="file"
            accept=".txt,.md,.py,.js,.csv"
            onChange={handleFileChange}
            disabled={isUploading}
            className="mt-4 block w-full text-sm text-slate-600 file:mr-4 file:rounded-lg file:border-0 file:bg-indigo-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-indigo-700 hover:file:bg-indigo-100 disabled:cursor-not-allowed disabled:opacity-60"
          />
        </label>

        {selectedFile && (
          <div className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-600">
            Selected:{" "}
            <span className="font-medium text-slate-900">
              {selectedFile.name}
            </span>{" "}
            ({formatBytes(selectedFile.size)})
          </div>
        )}

        <button
          type="submit"
          disabled={!selectedFile || isUploading}
          className="w-full rounded-lg bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isUploading
            ? "Processing file and generating embeddings..."
            : "Upload file"}
        </button>
      </form>

      {errorMessage && (
        <div className="mt-4 rounded-lg border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700">
          {errorMessage}
        </div>
      )}

      {uploadResult && (
        <div className="mt-5 rounded-xl border border-emerald-200 bg-emerald-50 p-4">
          <p className="text-sm font-semibold text-emerald-800">
            File uploaded and processed successfully.
          </p>

          <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
            <div>
              <dt className="text-emerald-700">Filename</dt>
              <dd className="font-medium text-slate-900">
                {uploadResult.filename}
              </dd>
            </div>
            <div>
              <dt className="text-emerald-700">File type</dt>
              <dd className="font-medium text-slate-900">
                {uploadResult.file_extension}
              </dd>
            </div>
            <div>
              <dt className="text-emerald-700">Size</dt>
              <dd className="font-medium text-slate-900">
                {formatBytes(uploadResult.size_bytes)}
              </dd>
            </div>
            <div>
              <dt className="text-emerald-700">Characters</dt>
              <dd className="font-medium text-slate-900">
                {uploadResult.character_count}
              </dd>
            </div>
            <div>
              <dt className="text-emerald-700">Chunks</dt>
              <dd className="font-medium text-slate-900">
                {uploadResult.chunk_count}
              </dd>
            </div>
            <div>
              <dt className="text-emerald-700">Embeddings</dt>
              <dd className="font-medium text-slate-900">
                {uploadResult.embedding_count}
              </dd>
            </div>
            <div>
              <dt className="text-emerald-700">Embedding dimension</dt>
              <dd className="font-medium text-slate-900">
                {uploadResult.embedding_dimension}
              </dd>
            </div>
          </dl>
        </div>
      )}
    </section>
  );
}
