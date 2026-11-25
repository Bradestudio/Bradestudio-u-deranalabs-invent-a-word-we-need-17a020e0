# make.fun bounty: u-deranalabs-invent-a-word-we-need-17a020e0
# Writes one invented English word and its one-line definition to
# /output/entry.txt.
#
# The entry: "plansigh — the quiet relief when someone else cancels plans
# you secretly hoped would fall through."
#
# plansigh (plan + sigh) names a gap English has no word for: the quiet,
# almost guilty relief when somebody else cancels plans you were dreading
# but would never cancel yourself. Everyone has felt it — the exhale when
# the message arrives, the evening suddenly yours again — yet no single word
# captures it. The coinage is sayable at once (plan-sigh, two familiar
# syllables), spellable exactly as it sounds, and memorable because the
# sigh is the feeling: the word performs its own meaning. The definition
# lands in one reading: "someone else cancels" does the work (you did not
# cancel, they did), "secretly hoped would fall through" names the part
# you would never admit out loud, and "quiet relief" keeps it honest —
# this is not triumph, it is a soft exhale.
#
# The competition gate is 1-140 characters, so it is enforced here, in
# code: length is counted in Unicode code points (not bytes), the text must
# be a single non-blank line, and the coined word must lead the line
# followed by its definition, so a future edit that breaks the form fails
# loudly instead of producing an invalid entry. The file is written
# atomically (temp file + rename) so /output/entry.txt is never left
# half-written.
import os

# Final entry (98 Unicode code points, one line):
# "plansigh — the quiet relief when someone else cancels plans you
# secretly hoped would fall through."
ENTRY = (
    "plansigh \u2014 the quiet relief when someone else cancels plans "
    "you secretly hoped would fall through."
)

# Competition gate: 1-140 Unicode code points, must contain non-space
# text, must be a single line, and must start with the coined word
# followed by an em dash and its one-line definition. Length is counted
# in Unicode code points (not UTF-8 bytes), so a future edit that makes
# the text too long (or empty, or multi-line) fails loudly instead of
# producing an invalid entry.
def validate_entry(text):
    length = len(text)
    if length < 1 or length > 140:
        raise ValueError(
            f"entry length {length} code points is outside the 1-140 range"
        )
    if text.strip() == "":
        raise ValueError("entry must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    word, sep, definition = text.partition("\u2014")
    if not sep or not word.strip() or not definition.strip():
        raise ValueError("entry must be '<word> — <definition>'")
    if len(word.strip().split()) != 1:
        raise ValueError("entry must coin exactly one word")
    return length


validate_entry(ENTRY)

os.makedirs("/output", exist_ok=True)
tmp_path = "/output/.entry.txt.tmp"
with open(tmp_path, "w", encoding="utf-8") as f:
    f.write(ENTRY)
os.replace(tmp_path, "/output/entry.txt")

# Read-back verification: confirm the bytes on disk are exactly the
# validated entry. A silent partial or corrupted write would otherwise
# go unnoticed, since os.replace succeeds once the temp file is in place.
with open("/output/entry.txt", encoding="utf-8") as f:
    written = f.read()
if written != ENTRY:
    raise ValueError(
        "read-back mismatch: /output/entry.txt does not match the validated entry"
    )
