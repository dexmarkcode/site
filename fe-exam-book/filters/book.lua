-- Book-wide Pandoc filter: boxes, part pages, chapter labels, drop caps.
local is_latex = FORMAT:match("latex") ~= nil

local box_titles = {
  tip = "Exam Tip", trap = "Common Trap", example = "Worked Example",
  handbook = "Using the Reference Handbook", keyidea = "Key Idea",
  objectives = "In This Chapter", story = "From the Study Desk",
  checklist = "Checklist", summary = "Chapter Summary",
}
local box_colours = {
  tip = "tipgreen", trap = "trapred", example = "inkblue", handbook = "copper",
  keyidea = "inkblue", objectives = "copper", story = "copper",
  checklist = "tipgreen", summary = "inkblue",
}

local function latex_escape(s)
  return (s:gsub("&", "\\&"):gsub("%%", "\\%%"))
end

function Span(el)
  if el.classes:includes("qtopic") and is_latex then
    local out = { pandoc.RawInline("latex", "\\qtopic{") }
    for _, i in ipairs(el.content) do table.insert(out, i) end
    table.insert(out, pandoc.RawInline("latex", "}"))
    return out
  end
end

function Div(el)
  for cls, title in pairs(box_titles) do
    if el.classes:includes(cls) then
      local t = el.attributes["title"] or title
      if is_latex then
        local out = { pandoc.RawBlock("latex", "\\begin{bookbox}{" .. latex_escape(t) .. "}{" .. box_colours[cls] .. "}") }
        for _, b in ipairs(el.content) do table.insert(out, b) end
        table.insert(out, pandoc.RawBlock("latex", "\\end{bookbox}"))
        return out
      else
        table.insert(el.content, 1, pandoc.Para({ pandoc.Span({ pandoc.Str(t) }, pandoc.Attr("", { "boxtitle" })) }))
        el.classes:insert("box")
        return el
      end
    end
  end
  if el.classes:includes("question") then
    if is_latex then
      local out = { pandoc.RawBlock("latex", "\\Needspace*{9\\baselineskip}\\begin{questionblock}") }
      for _, b in ipairs(el.content) do table.insert(out, b) end
      table.insert(out, pandoc.RawBlock("latex", "\\end{questionblock}"))
      return out
    end
    return el
  end
  if el.classes:includes("solution") then
    if is_latex then
      local out = { pandoc.RawBlock("latex", "\\begin{solutionblock}") }
      for _, b in ipairs(el.content) do table.insert(out, b) end
      table.insert(out, pandoc.RawBlock("latex", "\\end{solutionblock}"))
      return out
    end
    return el
  end
  if el.classes:includes("partpage") then
    local label = el.attributes["label"] or ""
    local title = el.attributes["title"] or ""
    if is_latex then
      local out = { pandoc.RawBlock("latex", "\\bookpart{" .. label .. "}{" .. latex_escape(title) .. "}{") }
      for _, b in ipairs(el.content) do table.insert(out, b) end
      table.insert(out, pandoc.RawBlock("latex", "}"))
      return out
    else
      local h = pandoc.Header(1, { pandoc.Span({ pandoc.Str("Part " .. label) }, pandoc.Attr("", { "partlabel" })), pandoc.LineBreak(), pandoc.Str(title) },
        pandoc.Attr("part-" .. label:lower(), { "part", "unnumbered" }))
      return { h, pandoc.Div(el.content, pandoc.Attr("", { "partblurb" })) }
    end
  end
  if el.classes:includes("bookmatter") and is_latex then
    return el.content
  end
end

local function dropcap(para)
  local first = para.content[1]
  if not first or first.t ~= "Str" then return para end
  local s = first.text
  local c = s:sub(1, 1)
  if not c:match("%a") then return para end
  local rest = s:sub(2)
  if is_latex then
    para.content[1] = pandoc.RawInline("latex", "\\lettrine{" .. c .. "}{" .. rest .. "}")
  else
    para.content[1] = pandoc.Span({ pandoc.Str(c) }, pandoc.Attr("", { "dropcap" }))
    table.insert(para.content, 2, pandoc.Str(rest))
  end
  return para
end

function Pandoc(doc)
  local chap, sec = 0, 0
  local want_drop = false
  local in_numbered = false
  local blocks = {}
  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 1 then
      local unnum = b.classes:includes("unnumbered") or b.classes:includes("part")
      if not unnum then
        chap = chap + 1
        sec = 0
        in_numbered = true
        if not is_latex then
          local content = { pandoc.Span({ pandoc.Str("Chapter " .. chap) }, pandoc.Attr("", { "chapnum" })), pandoc.LineBreak() }
          for _, i in ipairs(b.content) do table.insert(content, i) end
          b.content = content
        end
        want_drop = true
      else
        in_numbered = false
        want_drop = not b.classes:includes("part") and not b.classes:includes("nodrop")
        table.insert(blocks, b)
        if is_latex and not b.classes:includes("part") then
          table.insert(blocks, pandoc.RawBlock("latex", "\\markboth{" .. pandoc.utils.stringify(b.content) .. "}{" .. pandoc.utils.stringify(b.content) .. "}"))
        end
        goto continue
      end
      table.insert(blocks, b)
      goto continue
    elseif b.t == "Header" and b.level == 2 then
      want_drop = false
      if in_numbered and not b.classes:includes("unnumbered") then
        sec = sec + 1
        if not is_latex then
          table.insert(b.content, 1, pandoc.Span({ pandoc.Str(chap .. "." .. sec) }, pandoc.Attr("", { "secnum" })))
          table.insert(b.content, 2, pandoc.Space())
        end
      end
      table.insert(blocks, b)
      goto continue
    elseif b.t == "Para" and want_drop then
      want_drop = false
      table.insert(blocks, dropcap(b))
      goto continue
    elseif b.t == "Header" then
      want_drop = false
    end
    table.insert(blocks, b)
    ::continue::
  end
  doc.blocks = blocks
  return doc
end

function Math(el)
  if is_latex and el.mathtype == "DisplayMath" then
    return pandoc.RawInline("latex", "\\fitmath{" .. el.text .. "}")
  end
end

return {
  { Math = Math },
  { Span = Span },
  { Div = Div },
  { Pandoc = Pandoc },
}
