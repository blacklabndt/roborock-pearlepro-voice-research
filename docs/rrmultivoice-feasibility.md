# rrmultivoice feasibility for S5V / PearlEPro

Assessment date: 2026-10-26. This is a public-source assessment, not a device installation or confirmation of compatibility.

## Conclusion

`rrmultivoice` is a useful architectural reference for playing custom prompts through a robot's own speaker. It does not decode PearlEPro packages, create manufacturer-approved packages, or provide administrative access. No working S5V installation path has been established in this investigation.

The upstream README describes an older **Roborock S5** as the author's tested robot. That is not the **Qrevo S5V / a170** investigated here. Similar names are not compatibility evidence.

## Pinned source

Reviewed upstream commit: `ac5ae6efc99f2cdbfbe8cfff29077594d726ad78`.

- [README](https://github.com/erkexzcx/rrmultivoice/blob/ac5ae6efc99f2cdbfbe8cfff29077594d726ad78/README.md)
- [Command options](https://github.com/erkexzcx/rrmultivoice/blob/ac5ae6efc99f2cdbfbe8cfff29077594d726ad78/cmd/rrmultivoice/main.go)
- [Process discovery](https://github.com/erkexzcx/rrmultivoice/blob/ac5ae6efc99f2cdbfbe8cfff29077594d726ad78/pkg/rrmultivoice/pid.go)
- [File detection and replacement](https://github.com/erkexzcx/rrmultivoice/blob/ac5ae6efc99f2cdbfbe8cfff29077594d726ad78/pkg/rrmultivoice/linker.go)

No upstream source or bundled audio is redistributed here. The reviewed tree has no license file; reuse permissions should be clarified before distributing a derivative. Our repository's MIT license does not license upstream material.

## How it works

The program looks for a Linux process whose complete command line is exactly `RoboController` followed by a NUL byte. It polls that process's open file descriptors, by default every 300 ms, for paths in the configured sound directory. When it observes a new prompt filename, it removes that directory entry and creates a hard link to an alternative recording with the same filename.

The replacement happens when the file is observed open, not after a confirmed playback-completion event. A player retaining an open file descriptor would normally continue reading the old inode; a later open would see the replacement. Actual playback timing and caching need testing. Short opens can be missed by polling.

## Compatibility checklist

| Requirement | Upstream assumption | S5V evidence / status |
| --- | --- | --- |
| Execution access | README requires a rooted robot with SSH | No administrative shell or documented installation interface established |
| Operating system and CPU | Linux `/proc`; matching executable architecture | Not established for this device in this investigation |
| Playback process | Exact `RoboController` command line; not configurable | Not established |
| Sound location | Default `/opt/rockrobo/resources/sounds/en/`; configurable | Actual S5V paths not established |
| Filesystem permissions | Can remove and create sound-directory entries | Not established |
| Hard links | Source and destination on the same filesystem, with hard-link support | Not established |
| Audio format | Supplies individual recordings; no decoder or transcoder | Internal S5V codec, filenames and playback requirements remain unknown |
| Playback behavior | Individual files remain open long enough to detect | Not established; caching or a separate audio service could invalidate this approach |
| Service lifecycle | Device-specific startup configuration | Not established |

The official preview WAV format does not establish the internal recording format. Downloading an encrypted package or authenticating to the Roborock app does not satisfy the filesystem/execution requirements above.

## Source issues to resolve before any adaptation

These are static observations, not failures reproduced on a robot:

1. Replacement removes the destination before attempting the hard link. A missing source, permission error or filesystem mismatch can leave the prompt absent.
2. The source-existence check checks the pack directory rather than the individual recording. It therefore does not reliably skip packs missing that prompt.
3. Process discovery and error recovery recurse. Long-running failures can grow the call stack; a bounded iterative retry loop would be preferable.
4. Process selection is hard-coded, and the scan chooses the first matching descriptor. Multiple simultaneous files, different process command lines and cached playback need explicit handling.

## Practical next milestones

Follow-up: a separate [voice-message playback flow](voice-message-interface.md) was identified in the shared official plugin. Its S5V capability gate remains unverified. Checking this normal app feature is worthwhile before investing in a filesystem-based service.

1. **Compatibility evidence:** obtain documented information about the S5V execution environment and supported administrative or development interfaces. If an already authorized administrative interface becomes available, limit initial checks to OS/CPU, process identity, sound paths, mount properties and file metadata. No bypass or rooting workflow is proposed here.
2. **Desktop proof of concept:** independently implement and test the file-selection behavior against temporary directories and a simulated audio player. Require an observe-only mode, validation of every replacement, a temporary hard link followed by atomic rename, preservation of originals and clean rollback. This can be developed without touching a vacuum, but cannot prove S5V compatibility.
3. **Audio contract:** obtain a legitimately available plaintext example or documented playback specification to establish codec, sample rate, channels and event-to-filename mapping. Use original recordings for test assets.
4. **Device integration only after compatibility is established:** use a documented, authorized installation mechanism and verify recovery before changing playback files. If no such mechanism exists, the direct on-device route remains blocked regardless of desktop progress.

Success for the next stage is evidence that the S5V exposes a compatible, authorized playback integration point—not merely a binary that compiles for ARM. Full firmware replacement would expand the scope substantially and is not required by the rrmultivoice design.
