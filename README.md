# Pismo Disputes Workflow Presentation

An interactive HTML/CSS presentation that walks developers through the Pismo Disputes workflow system, including state machines, API patterns, and UI mockups.

## Features

- 18-slide presentation covering the complete disputes workflow
- Two-host narration (Alex - Technical Lead, Jordan - UX Specialist)
- ElevenLabs TTS audio with emotional delivery
- GSAP animations and transitions
- D3.js/dagre state machine visualizations
- React/Shadcn-style UI mockups
- Network-specific workflows (Visa, Mastercard, ELO)

## Running the Presentation

```bash
cd presentation
python -m http.server 8080
# Open http://localhost:8080 in your browser
```

Or simply open `presentation/index.html` in a modern browser.

## Controls

- **Arrow Keys**: Navigate slides
- **Space**: Play/pause audio
- **A**: Toggle auto-advance mode

## Project Structure

```
├── presentation/
│   ├── index.html          # Main presentation
│   └── assets/
│       └── audio/          # TTS audio files
├── research/               # Pismo API documentation
├── speaker-notes/          # Dialogue scripts
└── BRIEF.md               # Project requirements
```

## Disclaimer

**This presentation is for educational and demonstration purposes only.**

- All Pismo API information is sourced from the official documentation at [developers.pismo.io](https://developers.pismo.io)
- Pismo is a registered trademark of Pismo Solutions
- This project is **not affiliated with, endorsed by, or sponsored by Pismo**
- The UI mockups shown are conceptual designs and do not represent actual Pismo products
- Financial figures cited are from publicly available industry reports

## Sources

- [Pismo Disputes Overview](https://developers.pismo.io/pismo-docs/docs/disputes-overview)
- [Pismo Disputes State Machine](https://developers.pismo.io/pismo-docs/docs/disputes-state-machine)
- [Pismo API Reference](https://developers.pismo.io)

## License

This project is for educational purposes. Please refer to Pismo's official documentation for production implementations.
