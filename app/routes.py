{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "68acd869",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "from fastapi import APIRouter\n",
    "\n",
    "router = APIRouter()\n",
    "\n",
    "@router.get(\"/test\")\n",
    "def test():\n",
    "    return {\"message\": \"Test route works\"}\n"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
