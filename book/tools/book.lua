-- Pandoc filter: turns semantic divs into the book's LaTeX environments.
-- For EPUB/HTML the divs are kept and styled by CSS.

local is_latex = FORMAT:match('latex') ~= nil

local function raw(s) return pandoc.RawBlock('latex', s) end
local function rawi(s) return pandoc.RawInline('latex', s) end

local function inl_latex(inlines)
  return pandoc.write(pandoc.Pandoc({pandoc.Plain(inlines)}), 'latex'):gsub('\n$', '')
end

local boxes = {
  keyidea = 'Key idea', pitfall = 'Common pitfall', strategy = 'Problem-solving strategy',
  example = 'Worked example', objectives = 'In this chapter', remember = 'Remember',
  insight = 'From the lecture room',
}

function Header(el)
  if is_latex and el.level == 2 and el.classes:includes('unnumbered') then
    local t = inl_latex(el.content)
    return {el, raw('\\markboth{' .. t .. '}{' .. t .. '}')}
  end
  if el.level == 1 and el.classes:includes('part') then
    local title = pandoc.utils.stringify(el.content)
    if is_latex then
      if el.classes:includes('unnumbered') then
        return raw('\\bookpartx{' .. inl_latex(el.content) .. '}')
      end
      return raw('\\bookpart{' .. inl_latex(el.content) .. '}')
    end
  end
  return nil
end

function Span(el)
  if el.classes:includes('step') then
    if is_latex then
      return pandoc.List({rawi('\\steplabel{')}) .. el.content .. pandoc.List({rawi('}')})
    end
  end
  return nil
end

local function figure_latex(el)
  local img
  pandoc.walk_block(pandoc.Div(el.content), {Image = function(i) img = i end})
  if not img then return nil end
  local width = img.attributes.width or '88%'
  local w = width:match('^(%d+)%%$')
  local wtex = w and string.format('%.2f\\linewidth', tonumber(w) / 100) or width
  local cap = ''
  if el.caption and el.caption.long and #el.caption.long > 0 then
    cap = pandoc.write(pandoc.Pandoc(el.caption.long), 'latex'):gsub('\n+$', '')
  end
  return raw(string.format('\\bookfigure{%s.pdf}{%s}{%s}', img.src, wtex, cap))
end

function Figure(el)
  if is_latex then return figure_latex(el) end
  return nil
end

local function label(txt, cls)
  return pandoc.Para({pandoc.Span({pandoc.Strong({pandoc.Str(txt)})}, {class = cls})})
end

local function epub_div(el)
  local c = el.classes
  if c:includes('problem') then
    el.content:insert(1, label('Problem ' .. (el.attributes.num or '') .. ' · ' .. (el.attributes.level or ''), 'box-label'))
    return el
  end
  if c:includes('solution') then
    el.content:insert(1, label('Solution ' .. (el.attributes.num or ''), 'sol-label'))
    return el
  end
  if c:includes('answer') then
    el.content:insert(1, label('ANSWER', 'small-label'))
    return el
  end
  for cls, lab in pairs(boxes) do
    if c:includes(cls) then
      el.content:insert(1, label(string.upper(el.attributes.title or lab), 'small-label'))
      return el
    end
  end
  return nil
end

function Div(el)
  if not is_latex then return epub_div(el) end
  local c = el.classes
  if c:includes('partintro') then
    return pandoc.List({raw('\\begin{partintro}')}) .. el.content .. pandoc.List({raw('\\end{partintro}')})
  end
  if c:includes('problem') then
    local head = string.format('\\begin{problembox}{%s}{%s}{%s}', el.attributes.num or '',
      el.attributes.level or '', el.attributes.topic or '')
    return pandoc.List({raw(head)}) .. el.content .. pandoc.List({raw('\\end{problembox}')})
  end
  if c:includes('solution') then
    local head = string.format('\\begin{solutionblock}{%s}{%s}', el.attributes.num or '', el.attributes.topic or '')
    return pandoc.List({raw(head)}) .. el.content .. pandoc.List({raw('\\end{solutionblock}')})
  end
  if c:includes('restate') then
    return pandoc.List({raw('\\begin{restate}')}) .. el.content .. pandoc.List({raw('\\end{restate}')})
  end
  if c:includes('answer') then
    return pandoc.List({raw('\\begin{answerbox}')}) .. el.content .. pandoc.List({raw('\\end{answerbox}')})
  end
  if c:includes('dropcap') then
    local first = el.content[1]
    if first and first.t == 'Para' and first.content[1] and first.content[1].t == 'Str' then
      local word = first.content[1].text
      local L = word:sub(1, 1)
      local rest = word:sub(2)
      first.content[1] = rawi('\\lettrine{' .. L .. '}{' .. rest .. '}')
    end
    return el.content
  end
  for cls, label in pairs(boxes) do
    if c:includes(cls) then
      local title = el.attributes.title or label
      return pandoc.List({raw('\\begin{bookbox}{' .. cls .. '}{' .. title .. '}')}) .. el.content ..
        pandoc.List({raw('\\end{bookbox}')})
    end
  end
  return nil
end
